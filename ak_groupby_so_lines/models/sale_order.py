from collections import defaultdict
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit="sale.order"
    
    def _is_excluded_from_category_grouping(self, line):
        """
        The function checks if a given line should be excluded from category grouping based on certain
        conditions.
        
        :param line: The function `_is_excluded_from_category_grouping` takes two parameters: `self` and
        `line`. In this context, `line` seems to be an object representing a line item or a transaction.
        The function checks certain conditions related to the `line` object and returns `True` if
        :return: The function is checking various conditions and returning `True` if any of the
        conditions are met, otherwise it returns `False`.
        """
        if line.display_type:
            return True
        if getattr(line, "is_downpayment", False):
            return True
        if "is_delivery" in line._fields and line.is_delivery:
            return True
        return False

    def _get_eligible_product_lines(self):
        """
        This function returns the order lines that are not excluded from category grouping and have a
        product ID.
        :return: The method `_get_eligible_product_lines` is returning a filtered list of order lines.
        The filter condition checks if the order line is not excluded from category grouping and if it
        has a valid product ID.
        """
        return self.order_line.filtered(lambda l: not self._is_excluded_from_category_grouping(l) and l.product_id)

    def _get_excluded_lines(self):
        return self.order_line.filtered(self._is_excluded_from_category_grouping)

    def _groupby_so_lines_by_categ(self):
        for order_id in self:
            if self.env.context.get("ak_groupby_so_lines_skip"):
                continue
            if order_id.state not in ("draft", "sent","sale"):
                continue
            order_id._apply_category_grouping()

    def _apply_category_grouping(self):
        eligible_lines = self._get_eligible_product_lines()
        if not eligible_lines:
            return

        existing_sections = self.order_line.filtered(
            lambda l: l.display_type == "line_section" and l.category_section_id
        )
        sections_by_category = {}
        duplicate_sections = self.env["sale.order.line"]
        for section in existing_sections.sorted(lambda l: (l.sequence, l.id)):
            categ = section.category_section_id
            if categ.id in sections_by_category:
                duplicate_sections |= section
            else:
                sections_by_category[categ.id] = section

        # Determine category ordering:
        # - categories with an existing section follow the section's current sequence
        # - new categories are appended based on first appearance in eligible product lines
        category_order = []
        for section in existing_sections.sorted(lambda l: (l.sequence, l.id)):
            categ_id = section.category_section_id.id
            if categ_id and categ_id not in category_order:
                category_order.append(categ_id)
        for line in eligible_lines.sorted(lambda l: (l.sequence, l.id)):
            categ_id = line.product_id.categ_id.id
            if categ_id and categ_id not in category_order:
                category_order.append(categ_id)

        lines_by_category = defaultdict(lambda: self.env["sale.order.line"])
        for line in eligible_lines:
            lines_by_category[line.product_id.categ_id.id] |= line

        # Build desired order: [section + its lines] * N, then excluded lines at bottom.
        desired_lines = self.env["sale.order.line"]
        sequence = 10
        write_ops = []

        for categ_id in category_order:
            categ_lines = lines_by_category.get(categ_id, self.env["sale.order.line"])
            if not categ_lines:
                continue
            section = sections_by_category.get(categ_id)
            if not section:
                section = self.env["sale.order.line"].with_context(
                    ak_groupby_so_lines_skip=True,
                    sale_no_log_for_new_lines=True,
                ).create({
                    "order_id": self.id,
                    "display_type": "line_section",
                    "name": self.env["product.category"].browse(categ_id).name,
                    "sequence": sequence,
                    "category_section_id": categ_id,
                })
            else:
                section_vals = {
                    "sequence": sequence,
                    "name": section.category_section_id.name,
                }
                write_ops.append((section, section_vals))

            desired_lines |= section
            sequence += 10

            for line in categ_lines.sorted(lambda l: (l.sequence, l.id)):
                desired_lines |= line
                write_ops.append((line, {"sequence": sequence}))
                sequence += 10

        categories_with_lines = set(lines_by_category.keys())
        empty_sections = existing_sections.filtered(lambda l: l.category_section_id.id not in categories_with_lines)
        sections_to_delete = (empty_sections | duplicate_sections)

        # Move any other remaining lines (excluded + anything unexpected) to bottom, preserving their relative order.
        remaining_lines = (self.order_line - desired_lines - sections_to_delete).sorted(lambda l: (l.sequence, l.id))
        for line in remaining_lines:
            write_ops.append((line, {"sequence": sequence}))
            sequence += 10

        if sections_to_delete:
            sections_to_delete.with_context(ak_groupby_so_lines_skip=True).unlink()

        for line, vals in write_ops:
            line.with_context(ak_groupby_so_lines_skip=True).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        order_ids = super().create(vals_list)
        order_ids._groupby_so_lines_by_categ()
        return order_ids

    def write(self, vals):
        res = super().write(vals)
        self._groupby_so_lines_by_categ()
        return res
        

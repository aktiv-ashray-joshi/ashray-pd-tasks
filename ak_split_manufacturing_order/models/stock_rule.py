from collections import defaultdict
from odoo import api, models, SUPERUSER_ID

class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_manufacture(self, procurements):
        sale_procs = []
        regular_procs = []
        for p, rule in procurements:
            is_sale = bool(p.values.get('sale_line_id'))
            if is_sale:
                sale_procs.append((p, rule))
            else:
                regular_procs.append((p, rule))
        
        res = True
        if regular_procs:
            res = super()._run_manufacture(regular_procs)
            
        # 2. Handle Sale Order procurements with forced batching (batch_size = 1 unit)
        if not sale_procs:
            return res
            
        new_productions_values_by_company = defaultdict(lambda: defaultdict(list))
        for procurement, rule in sale_procs:
            if procurement.product_uom.compare(procurement.product_qty, 0) <= 0:
                continue
            bom = rule._get_matching_bom(procurement.product_id, procurement.company_id, procurement.values)
            
            # Since it's from a Sale, we force batch_size to 1 and ALWAYS create new MOs
            procurement_qty = procurement.product_qty
            
            vals = rule._prepare_mo_vals(*procurement, bom)
            while procurement.product_uom.compare(procurement_qty, 0) > 0:
                split_qty = min(1.0, procurement_qty)
                prod_qty = procurement.product_uom._compute_quantity(split_qty, bom.product_uom_id) if bom else split_qty
                
                new_productions_values_by_company[procurement.company_id.id]['values'].append({
                    **vals,
                    'product_qty': prod_qty,
                })
                new_productions_values_by_company[procurement.company_id.id]['procurements'].append(procurement)
                procurement_qty -= 1.0

        for company_id in new_productions_values_by_company:
            productions_vals_list = new_productions_values_by_company[company_id]['values']
            productions = self.env['mrp.production'].with_user(SUPERUSER_ID).sudo().with_company(company_id).create(productions_vals_list)
            for mo in productions:
                if self._should_auto_confirm_procurement_mo(mo):
                    mo.action_confirm()
            productions._post_run_manufacture(new_productions_values_by_company[company_id]['procurements'])
            
        return res

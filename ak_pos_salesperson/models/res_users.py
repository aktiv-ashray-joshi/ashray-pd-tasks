from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_pos_salesperson = fields.Boolean(string="Is POS Salesperson")

    @api.model
    def _load_pos_data_domain(self, data, config):
        """
        By default, pos.order user_id loading domain is only the current user.
        We extend this to also include any user where is_pos_salesperson is True.
        """
        return ['|', ('id', '=', self.env.uid), ('is_pos_salesperson', '=', True)]

    @api.model
    def _load_pos_data_fields(self, config):
        """Extend the fields loaded for res.users in the POS."""
        res = super()._load_pos_data_fields(config)
        res.extend(['is_pos_salesperson', 'phone', 'email'])
        return res

    @api.model
    def _load_pos_data_search_read(self, data, config):
        """Load res.users for POS, bypassing access rules for allowed dataset."""
        # Do not apply the "last_server_date" restriction for salespersons: the POS must
        # always have the full set of selectable users, not only the ones modified since
        # last sync.
        domain = self._load_pos_data_domain(data, config)
        if domain is False:
            return []
        records = self.sudo().search(domain)
        return self._load_pos_data_read(records, config)

    @api.model
    def _load_pos_data_read(self, records, config):
        """Read res.users for POS without _filtered_access('read') dropping records."""
        fields = self._load_pos_data_fields(config)
        read_records = records.sudo().read(fields, load=False) or []

        for rec in read_records:
            all_group_ids = rec.get('all_group_ids') or []
            if rec.get('id') == self.env.uid:
                rec['_role'] = 'manager' if config.group_pos_manager_id.id in all_group_ids else 'cashier'
            rec.pop('all_group_ids', None)

        return read_records

    def onchange(self, values, field_names, fields_spec):
        if self.env.context.get("pos_salesperson_manage"):
            if not self.env.user.has_group("point_of_sale.group_pos_manager"):
                return super().onchange(values, field_names, fields_spec)
            return super(ResUsers, self.sudo()).onchange(values, field_names, fields_spec)
        return super().onchange(values, field_names, fields_spec)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get("pos_salesperson_manage"):
            if not self.env.user.has_group("point_of_sale.group_pos_manager"):
                return super().create(vals_list)
            vals_list = [dict(vals, is_pos_salesperson=True) for vals in vals_list]
            return super(ResUsers, self.sudo()).create(vals_list)
        return super().create(vals_list)

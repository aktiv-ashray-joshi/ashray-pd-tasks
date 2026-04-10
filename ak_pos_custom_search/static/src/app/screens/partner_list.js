import { PartnerList } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";

patch(PartnerList.prototype, {
    async getNewPartners() {
        const originalCallRelated = this.pos.data.callRelated;
        this.pos.data.callRelated = async (model, method, args) => {
            if (model === "res.partner" && method === "get_new_partner" && this.state.query) {
                args[1] = ['|', ['ak_customer_code', 'ilike', this.state.query + '%'], ...args[1]];
            }
            return originalCallRelated.apply(this.pos.data, [model, method, args]);
        };
        try {
            return await super.getNewPartners();
        } finally {
            this.pos.data.callRelated = originalCallRelated;
        }
    }
});

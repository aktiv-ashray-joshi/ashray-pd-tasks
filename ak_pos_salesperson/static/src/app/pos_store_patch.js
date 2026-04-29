import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    set_salesperson(user_id) {
        this.uiState = this.uiState || {};
        // "Unselect" should only clear the UI selection. Keep `user_id` as-is
        // (it is normally the logged-in cashier) to avoid breaking backend expectations.
        if (!user_id) {
            this.uiState.ak_salesperson_selected = false;
            this.update({}, { omitUnknownField: true });
            return;
        }
        this.uiState.ak_salesperson_selected = true;
        this.update({ user_id }, { omitUnknownField: true });
    },

    get_salesperson_name() {
        if (!this.uiState?.ak_salesperson_selected) {
            return false;
        }
        return this.user_id?.name || false;
    },
});

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SalespersonList } from "@ak_pos_salesperson/app/salesperson_list/salesperson_list";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class SelectSalespersonButton extends Component {
    static template = "ak_pos_salesperson.SelectSalespersonButton";
    static props = { "*": true };
    
    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
    }

    get currentOrder() {
        return this.pos.getOrder();
    }

    get salespersonName() {
        if (!this.currentOrder) return false;
        return this.currentOrder.get_salesperson_name();
    }

    async clickSelectSalesperson() {
        const order = this.currentOrder;
        if (!order) return;

        const allUsers = this.pos.models["res.users"].getAll();
        const salespersons = allUsers.filter(u => u.is_pos_salesperson);

        if (salespersons.length === 0) {
            this.dialog.add(AlertDialog, {
                title: _t("No Salespersons Found"),
                body: _t("There are currently no users marked as POS Salesperson."),
            });
            return;
        }

        const selectedSalespersonId = await makeAwaitable(this.dialog, SalespersonList, {
            salespersons: salespersons,
            currentSalespersonId: order.user_id?.id || false,
        });

        if (selectedSalespersonId === false) {
            order.set_salesperson(false);
        } else if (selectedSalespersonId !== undefined) {
            order.set_salesperson(selectedSalespersonId);
        }
    }
}

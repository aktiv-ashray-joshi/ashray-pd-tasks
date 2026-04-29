import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { Input } from "@point_of_sale/app/components/inputs/input/input";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { makeActionAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

export class SalespersonList extends Component {
    static components = { Dialog, Input };
    static template = "ak_pos_salesperson.SalespersonList";
    static props = {
        salespersons: { type: Array },
        currentSalespersonId: { optional: true },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.pos = usePos();
        this.ui = useService("ui");
        this.state = useState({ query: "" });
    }

    async createSalesperson() {
        const record = await makeActionAwaitable(
            this.pos.action,
            "ak_pos_salesperson.res_users_action_edit_pos_salesperson",
            {
                additionalContext: {
                    pos_salesperson_manage: true,
                    default_is_pos_salesperson: true,
                },
            }
        );
        if (!record?.evalContext?.id) {
            return;
        }
        // Use the POS data service so the created user is also stored in IndexedDB.
        const [user] = await this.pos.data.read("res.users", [record.evalContext.id]);
        if (user) {
            this.clickSalesperson(user);
        }
    }

    get filteredSalespersons() {
        const query = this.state.query.toLowerCase();
        if (!query) return this.props.salespersons;
        return this.props.salespersons.filter(
            (user) =>
                (user.name && user.name.toLowerCase().includes(query)) ||
                (user.email && user.email.toLowerCase().includes(query)) ||
                (user.phone && user.phone.toLowerCase().includes(query))
        );
    }

    clickSalesperson(user) {
        this.props.getPayload(user.id);
        this.props.close();
    }

    clickUnselect() {
        this.props.getPayload(false);
        this.props.close();
    }
}

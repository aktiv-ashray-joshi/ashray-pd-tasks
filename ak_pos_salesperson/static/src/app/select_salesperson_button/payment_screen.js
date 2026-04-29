import { SelectSalespersonButton } from "@ak_pos_salesperson/app/select_salesperson_button/select_salesperson_button";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalespersonButton,
    },
});

patch(PaymentScreen, {
    components: {
        ...PaymentScreen.components,
        SelectSalespersonButton,
    },
});


import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

export class ProductRemoveConfirm extends Interaction {

    static selector = ".ak_product_remove_btn";

    dynamicContent = {
        _root: { "t-on-click.prevent": this.onClick },
    };

    onClick(ev) {
        const btn = ev.currentTarget;

        const formId = btn.dataset.formId;
        const productName = btn.dataset.productName || _t("this product");

        this.services.dialog.add(ConfirmationDialog, {
            title: _t("Remove Product"),
            body: _t(
                'Are you sure you want to remove "%s" from this category?',
                productName
            ),
            confirmLabel: _t("Remove"),
            cancelLabel: _t("Cancel"),

            confirm: () => {
                const form = document.getElementById(formId);
                if (form) {
                    form.submit();
                }
            },

            cancel: () => {},
        });
    }
}

registry
    .category("public.interactions")
    .add("ak_portal_product_category.product_remove_confirm", ProductRemoveConfirm);

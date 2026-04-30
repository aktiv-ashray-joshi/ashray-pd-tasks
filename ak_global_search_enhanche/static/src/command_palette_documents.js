import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const commandCategoryRegistry = registry.category("command_categories");
const commandProviderRegistry = registry.category("command_provider");

const DOCUMENTS_CATEGORY = "ak_global_search_documents";
commandCategoryRegistry.add(
    DOCUMENTS_CATEGORY,
    { namespace: "/", name: _t("Documents") },
    { sequence: 35 }
);

let rulesPromise;
async function fetchRules() {
    if (!rulesPromise) {
        rulesPromise = rpc("/ak_global_search_enhanche/rules", {});
    }
    return rulesPromise;
}

async function safeSearchRead(orm, model, domain, fields, limit) {
    try {
        return await orm.searchRead(model, domain, fields, { limit });
    } catch {
        return [];
    }
}

function buildOrDomain(fieldNames, term) {
    const conditions = fieldNames.map((fieldName) => [fieldName, "ilike", term]);
    if (conditions.length <= 1) {
        return conditions;
    }
    const domain = [];
    for (let i = 0; i < conditions.length - 1; i++) {
        domain.push("|");
    }
    domain.push(...conditions);
    return domain;
}

function openRecordAction(env, model, id) {
    return env.services.action.doAction({
        type: "ir.actions.act_window",
        res_model: model,
        res_id: id,
        views: [[false, "form"]],
        target: "current",
    });
}

function recordHref(model, id) {
    return `#id=${id}&model=${encodeURIComponent(model)}&view_type=form`;
}

commandProviderRegistry.add("ak_global_search_documents", {
    namespace: "/",
    async provide(env, options = {}) {
        const searchValue = (options.searchValue || "").trim();
        if (!searchValue || searchValue.length < 2) {
            return [];
        }

        const orm = env.services.orm;
        const limitPerModel = 7;

        const rules = await fetchRules();
        if (!rules.length) {
            return [];
        }

        const commands = [];

        const resultsByRule = await Promise.all(
            rules.map((rule) => {
                const domain = buildOrDomain(rule.fields || [], searchValue);
                if (!domain.length) {
                    return Promise.resolve({ model: rule.model, name: rule.name, records: [] });
                }
                return safeSearchRead(orm, rule.model, domain, ["display_name"], limitPerModel).then(
                    (records) => ({ model: rule.model, name: rule.name, records })
                );
            })
        );

        for (const { model, name, records } of resultsByRule) {
            for (const rec of records) {
                commands.push({
                    category: DOCUMENTS_CATEGORY,
                    name: name ? `${name}: ${rec.display_name}` : rec.display_name,
                    href: recordHref(model, rec.id),
                    action: () => openRecordAction(env, model, rec.id),
                });
            }
        }

        return commands;
    },
});

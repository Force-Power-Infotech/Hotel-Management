frappe.provide("erpnext.PointOfSale");

frappe.pages["point-of-sale"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Point of Sale"),
		single_column: true,
	});

	frappe.require("point-of-sale.bundle.js", function () {
		wrapper.pos = new erpnext.PointOfSale.Controller(wrapper);

		setTimeout(() => {
			add_custom_pos_button(wrapper.pos);
		}, 1000);
	});
};

function add_custom_pos_button(controller) {

	controller.page.add_menu_item(__("Sell on Credit"), () => {
		const doc = controller.frm.doc;

		if (!doc.customer || !doc.items?.length) {
			frappe.msgprint("Please select a customer and add at least one item.");
			return;
		}

		const invoice_data = {
			customer: doc.customer,
			items: doc.items.map(item => ({
				item_code: item.item_code,
				qty: item.qty,
				rate: item.rate,
				uom: item.uom,
				conversion_factor: item.conversion_factor,
			}))
		};

		frappe.call({
			method: "hospitality.hospitality.custom.pos_invoice.pos_invoice.sell_on_credit",
			args: {
				invoice_data: JSON.stringify(invoice_data),
			},
			callback: function (r) {
				if (!r.exc && r.message) {

					window.location.reload();

				}
			},
		});
	});
}

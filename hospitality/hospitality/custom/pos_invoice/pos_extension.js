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
			add_custom_pos_buttons(wrapper.pos);
		}, 1000);
	});
};

function add_custom_pos_buttons(controller) {

	controller.page.add_menu_item(__("Sell on Credit"), () => {
		const doc = controller.frm.doc;

		if (!doc.customer || !doc.items?.length) {
			frappe.msgprint("Please select a customer and add at least one item.");
			return;
		}

		const invoice_data = {
			customer: doc.customer,
			pos_profile: doc.pos_profile,
			taxes_and_charges: doc.taxes_and_charges || null,
			// taxes: doc.taxes?.map(tax => ({
			// 	charge_type: tax.charge_type,
			// 	account_head: tax.account_head,
			// 	description: tax.description,
			// 	rate: tax.rate,
			// 	cost_center: tax.cost_center,
			// 	tax_amount: tax.tax_amount,
			// 	tax_amount_after_discount_amount: tax.tax_amount_after_discount_amount,
			// 	base_tax_amount: tax.base_tax_amount,
			// 	base_tax_amount_after_discount_amount: tax.base_tax_amount_after_discount_amount,
			// 	item_wise_tax_detail: tax.item_wise_tax_detail,
			// })) || [],
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

					const link = `<a href="/app/sales-invoice/${r.message}" style="font-weight: bold;">${r.message}</a>`;
					frappe.msgprint({
						title: __("Sales Invoice Created"),
						message: `Sales Invoice Created: ${link}`,
						indicator: "green"
					});

				}
			},
		});
	});

	controller.page.add_menu_item(__("Add to Room Bill"), () => {
		const doc = controller.frm.doc;

		if (!doc.customer || !doc.items?.length) {
			frappe.msgprint("Please select a customer and add at least one item.");
			return;
		}

		const invoice_data = {
			customer: doc.customer,
			pos_profile: doc.pos_profile,
			taxes_and_charges: doc.taxes_and_charges || null,
			items: doc.items.map(item => ({
				item_code: item.item_code,
				qty: item.qty,
				rate: item.rate,
				uom: item.uom,
				conversion_factor: item.conversion_factor,
			}))
		};

		frappe.call({
			method: "hospitality.hospitality.custom.pos_invoice.pos_invoice.add_to_room_bill",
			args: {
				invoice_data: JSON.stringify(invoice_data),
			},
			freeze : true,
			freezeMessage : "Please wait...",
			callback: function (r) {
				if (r.message) {

					const link = `<a href="/app/sales-invoice/${r.message.invoice}" style="font-weight: bold;">${r.message.invoice}</a>`;
					frappe.msgprint({
						title: __("Bill Attached to Room"),
						message: `Sales Invoice Updated: ${link} for Room Reservation : ${r.message.roomId}`,
						indicator: "green"
					});
					window.location.reload();
				}
			},
		});
	});

	controller.page.add_menu_item(__("Reload"), () => {
		window.location.reload();
	});
}

// Copyright (c) 2025, Admin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Reservation', {
	onload(frm) {
		update_field_requirements(frm);
		set_default_posting_values(frm);
		toggle_posting_time_fields(frm);
	},

	refresh(frm) {
		update_field_requirements(frm);
		toggle_posting_time_fields(frm);

		if (frm.doc.docstatus === 1) {
			frm.set_df_property('set_posting_time', 'hidden', 1);
		}
	},

	validate(frm) {
		validate_people_count(frm);
		validate_checkin_checkout_dates(frm);

		return new Promise((resolve, reject) => {
			frappe.call({
				method: "hospitality.guest_house.doctype.room_reservation.room_reservation.check_room_availability",
				args: {
					room: frm.doc.hotel_room_number,
					check_in: frm.doc.checkin_date,
					check_out: frm.doc.checkout_date,
					current_docname: frm.doc.name
				},
				callback: function (r) {
					if (r.message === true) {
						frappe.throw(__('The selected room is already booked for the given dates.'));
						reject();
					} else {
						resolve();
					}
				}
			});
		});
	},

	guest(frm) {
		clear_party_details(frm);
		update_field_requirements(frm);
		clear_contact_info(frm);
	},

	member_id(frm) {
		if (frm.doc.member_id) {
			fetch_party_details('Member Details', frm.doc.member_id, frm);
		}
	},

	guest_id(frm) {
		if (frm.doc.guest_id) {
			fetch_party_details('Guest Details', frm.doc.guest_id, frm);
		}
	},

	hotel_room_type(frm) {
		if (frm.doc.hotel_room_type) {
			frm.set_query('hotel_room_number', () => {
				return {
					filters: {
						room_type: frm.doc.hotel_room_type
					}
				};
			});

			if (frm.doc.hotel_room_number) {
				frm.set_value('hotel_room_number', '');
			}
		} else {
			frm.set_query('hotel_room_number', () => {
				return {};
			});
		}
	},

	hotel_room_number(frm) {
		if (!frm.doc.hotel_room_type && frm.doc.hotel_room_number) {
			frappe.db.get_value('Hotel Room', frm.doc.hotel_room_number, 'room_type')
				.then(r => {
					if (r && r.message && r.message.room_type) {
						frm.set_value('hotel_room_type', r.message.room_type);
					}
				});
		}
	},

	sales_item(frm) {
		frappe.call({
			method: "hospitality.guest_house.doctype.room_reservation.room_reservation.get_valid_item_price",
			args: {
				item_code: frm.doc.sales_item,
				price_list: "Standard Selling"
			},
			callback: (r) => {
				if (r.message) {
					frm.set_value("hotel_room_price", r.message);
				}
			}
		});
	},

	set_posting_time(frm) {
		toggle_posting_time_fields(frm);
	},

	before_save(frm) {
		if (!frm.doc.set_posting_time) {
			frm.set_value('posting_date', frappe.datetime.get_today());
			frm.set_value('posting_time', frappe.datetime.now_time());
		}
	}

});

function update_field_requirements(frm) {
	const is_guest = frm.doc.guest;

	frm.set_df_property('guest_id', 'reqd', is_guest);
	frm.set_df_property('member_id', 'reqd', !is_guest);
}

function clear_party_details(frm) {
	if (frm.doc.guest) {
		frm.set_value('member_id', '');
		frm.set_value('member_name', '');
	} else {
		frm.set_value('guest_id', '');
		frm.set_value('guest_name', '');
	}
}

function clear_contact_info(frm) {
	frm.set_value('contact_number', '');
	frm.set_value('email_address', '');
}

function fetch_party_details(doctype, name, frm) {
	frappe.db.get_doc(doctype, name)
		.then(doc => {
			frm.set_value('contact_number', doc.contact_number || '');
			frm.set_value('email_address', doc.email_address || '');
			frm.set_value('preference', doc.stay_preference || '');
		});
}

function validate_people_count(frm) {
	if (frm.doc.number_of_people) {
		const entered = frm.doc.number_of_people;
		const rows = frm.doc.details_of_people.length;

		if (rows < entered) {
			const $wrapper = frm.fields_dict.details_of_people.$wrapper;

			$wrapper.css("border", "2px solid red");
			frappe.utils.scroll_to(frm.fields_dict.details_of_people.wrapper);

			setTimeout(() => {
				$wrapper.fadeOut(300, () => {
					$wrapper.css("border", "none").fadeIn(300);
				});
			}, 5000);

			frappe.throw(`You have entered ${entered} as the number of people, but only ${rows} detail(s) provided. <br> Add ${entered - rows} more person(s) details.`);
		} else if (rows > entered) {
			frappe.throw(`You have entered ${entered} as the number of people, but added ${rows} detail(s)!`);
		}
	}
}

function set_default_posting_values(frm) {
	if (!frm.doc.posting_date) {
		frm.set_value('posting_date', frappe.datetime.get_today());
	}
	if (!frm.doc.posting_time) {
		frm.set_value('posting_time', frappe.datetime.now_time());
	}
}

function toggle_posting_time_fields(frm) {
	const editable = frm.doc.set_posting_time === 1;

	frm.set_df_property('posting_date', 'read_only', !editable);
	frm.set_df_property('posting_time', 'read_only', !editable);
}

function validate_checkin_checkout_dates(frm) {
	const checkin = frm.doc.checkin_date;
	const checkout = frm.doc.checkout_date;

	if (checkin && checkout) {
		const checkinDate = new Date(checkin);
		const checkoutDate = new Date(checkout);

		if (checkoutDate <= checkinDate) {
			frappe.utils.scroll_to(frm.fields_dict.checkout_date.wrapper);
			frappe.throw("Checkout Date must be after Check-in Date.");
		}
	}
}

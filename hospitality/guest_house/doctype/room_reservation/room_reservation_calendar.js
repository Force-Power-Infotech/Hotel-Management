frappe.views.calendar["Room Reservation"] = {
	field_map: {
		"start": "checkin_date",
		"end": "checkout_date",
		"id": "name",
		"title": "hotel_room_number",
		"allDay": 1,
		"eventColor": "color"
	},
	order_by: "checkin_date",
	get_events_method: "hospitality.guest_house.doctype.room_reservation.room_reservation.get_events"
};

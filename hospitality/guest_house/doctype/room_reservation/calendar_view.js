// frappe.views.calendar["Sales Order"] = {
// 	field_map: {
// 		start: "delivery_date",
// 		end: "delivery_date",
// 		id: "name",
// 		title: "customer_name",
// 		allDay: "allDay",
// 		convertToUserTz: "convertToUserTz",
// 	},
// 	gantt: true,
// 	filters: [
// 		{
// 			fieldtype: "Link",
// 			fieldname: "customer",
// 			options: "Customer",
// 			label: __("Customer"),
// 		},
// 		{
// 			fieldtype: "Select",
// 			fieldname: "delivery_status",
// 			options: "Not Delivered\nFully Delivered\nPartly Delivered\nClosed\nNot Applicable",
// 			label: __("Delivery Status"),
// 		},
// 		{
// 			fieldtype: "Select",
// 			fieldname: "billing_status",
// 			options: "Not Billed\nFully Billed\nPartly Billed\nClosed",
// 			label: __("Billing Status"),
// 		},
// 	],
// 	get_events_method: "erpnext.selling.doctype.sales_order.sales_order.get_events",
// 	get_css_class: function (data) {
// 		if (data.status == "Closed") {
// 			return "success";
// 		}
// 		if (data.delivery_status == "Not Delivered") {
// 			return "danger";
// 		} else if (data.delivery_status == "Partly Delivered") {
// 			return "warning";
// 		} else if (data.delivery_status == "Fully Delivered") {
// 			return "success";
// 		}
// 	},
// };

// frappe.views.calendar["Sales Order"] = {
//     field_map: {
//         start: "delivery_date",
//         end: "delivery_date",
//         id: "name",
//         title: "customer_name",
//         allDay: "allDay",
//         convertToUserTz: "convertToUserTz",
//     },
//     gantt: true,
//     filters: [
//         {
//             fieldtype: "Link",
//             fieldname: "customer",
//             options: "Customer",
//             label: __("Customer"),
//         },
//         {
//             fieldtype: "Select",
//             fieldname: "delivery_status",
//             options: "Not Delivered\nFully Delivered\nPartly Delivered\nClosed\nNot Applicable",
//             label: __("Delivery Status"),
//         },
//         {
//             fieldtype: "Select",
//             fieldname: "billing_status",
//             options: "Not Billed\nFully Billed\nPartly Billed\nClosed",
//             label: __("Billing Status"),
//         },
//     ],
//     get_events_method: "erpnext.selling.doctype.sales_order.sales_order.get_events",
//     get_css_class: function (data) {
        
//         const roomColors = {
//             "100": "color-1", 
//             "101": "color-2",
//             "102": "color-3",
//             "103": "color-4",
//         };

//         if (data.hotel_room_number && roomColors[data.hotel_room_number]) {
//             return roomColors[data.hotel_room_number];
//         }

//         if (data.status == "Closed") {
//             return "success";
//         }
//         if (data.delivery_status == "Not Delivered") {
//             return "danger";
//         } else if (data.delivery_status == "Partly Delivered") {
//             return "warning";
//         } else if (data.delivery_status == "Fully Delivered") {
//             return "success";
//         }

//         return ""; 
//     },
// };
frappe.views.calendar["Room Reservation"] = {
    field_map: {
        start: "checkin_date",
        end: "checkout_date",
        id: "hotel_room_number",
        title: "Hotel Room Number",
        allDay: "allDay",
        convertToUserTz: "convertToUserTz",
    },
    gantt: true,
    // filters: [
        // {
        //     fieldtype: "Link",
        //     fieldname: "customer",
        //     options: "Customer",
        //     label: __("Customer"),
        // },
        // {
        //     fieldtype: "Select",
        //     fieldname: "delivery_status",
        //     options: "Not Delivered\nFully Delivered\nPartly Delivered\nClosed\nNot Applicable",
        //     label: __("Delivery Status"),
        // },
        // {
        //     fieldtype: "Select",
        //     fieldname: "billing_status",
        //     options: "Not Billed\nFully Billed\nPartly Billed\nClosed",
        //     label: __("Billing Status"),
        // },
    // ],
    // get_events_method: "erpnext.selling.doctype.sales_order.sales_order.get_events",
    get_css_class: function (data) {
        const roomColors = {
            "100": "color-1",
            "101": "color-2",
            "102": "color-3",
            "103": "color-4",
        };

        return roomColors[data.hotel_room_number] || ""; // Fallback if no match
    },
};

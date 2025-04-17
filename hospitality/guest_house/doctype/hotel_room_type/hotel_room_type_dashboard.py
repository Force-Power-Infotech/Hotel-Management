import frappe
from frappe import _

def get_data():
    def get_preferences_data():
        # Fetch counts of Room Reservations grouped by preferences for the current Room Type
        hotel_room_type = frappe.form_dict.get("name") or "Premium" # Get the current Hotel Room Type
        if not hotel_room_type:
            return []  # Return empty if no room type is provided

        # SQL Query to get counts of Room Reservations grouped by preferences
        result = frappe.db.sql("""
            SELECT 
                preference, 
                COUNT(name) AS count
            FROM 
                `tabRoom Reservation`
            WHERE 
                hotel_room_type = %(hotel_room_type)s
                AND docstatus = 0
            GROUP BY 
                preference
        """, {
            "hotel_room_type": hotel_room_type
        }, as_dict=True)
        print(result)
        # Define the possible preferences
        preferences = ["View", "Smoking", "Late Checkout"]
        items = []

        # Create dashboard badges for each preference with counts
        for pref in preferences:
            count = next((r['count'] for r in result if r['preference'] == pref), 0)
            items.append({
                "type": "link",
                "name": pref,
                "label": _(pref),
                "count": count,
                "doctype": "Room Reservation",
                "filters": {
                    "hotel_room_type": hotel_room_type,
                    "preference": pref,
                    "docstatus": 1
                }
            })

        # return items
        return [
            {"label": pref['preference'], "value": pref['count']}
            for pref in items
        ]

    # print(get_preferences_data())

    return {
        "fieldname": "hotel_room_type",  # Links Room Reservation to Hotel Room Type
        "non_standard_fieldnames": {},
        "transactions": [
            {
                "label": _("Room Reservations"),
                "items": ["Room Reservation"]
            },{
                "label": _("Room Type"),
                "items": ["Room Type"]
            },{
                "label": _("Room Type Preferences"),
                "items": ["Room Type Preferences"]  
            },{
                "label": _("Room Type Rates"),
                "items": ["Room Type Rates"]
            },{
                "label": _("Room Type Amenities"),
                "items": ["Room Type Amenities"]
            },{
                "label": _("Room Type Images"),
                "items": ["Room Type Images"]
            },{
                "label": _("Room Type Booking"),
                "items": ["Room Type Booking"]
            },{
                "label": _("Room Type Booking Preferences"),
                "items": ["Room Type Booking Preferences"]
            }
        ],
        "stats": {
            "label": _("Preferences"),
            # "items": get_preferences_data()
            "items": [
                {
                    "type": "link",
                    "name": "View",
                    "label": _("View"),
                    "count": 0,
                    "doctype": "Room Reservation",
                    "filters": {
                        "hotel_room_type": frappe.form_dict.get("name") or "Premium",
                        "preference": "View",
                        "docstatus": 1
                    }
                },
                {
                    "type": "link",
                    "name": "Smoking",
                    "label": _("Smoking"),
                    "count": 0,
                    "doctype": "Room Reservation",
                    "filters": {
                        "hotel_room_type": frappe.form_dict.get("name") or "Premium",
                        "preference": "Smoking",
                        "docstatus": 1
                    }
                },
                {
                    "type": "link",
                    "name": "Late Checkout",
                    "label": _("Late Checkout"),
                    "count": 0,
                    "doctype": "Room Reservation",
                    "filters": {
                        "hotel_room_type": frappe.form_dict.get("name") or "Premium",
                        "preference": "Late Checkout",
                        "docstatus": 1
                    }
                }
            ]
        }
    }

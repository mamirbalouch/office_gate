import frappe

def execute():
    doctype = "Travel Itinerary"
    fieldname = "mode_of_travel"

    # Required options in correct order (excluding blank)
    required_options = ["Vehicle", "Flight", "Train", "Taxi"]

    # Fetch existing Property Setter
    ps = frappe.db.get_value(
        "Property Setter",
        {
            "doc_type": doctype,
            "field_name": fieldname,
            "property": "options"
        },
        ["name", "value"],
        as_dict=True
    )

    if ps:
        # Property Setter exists → merge and update
        existing = ps.value.split("\n")

        # Normalize existing list by removing whitespace
        existing = [opt.strip() for opt in existing if opt is not None]

        # Always ensure blank first line
        new_list = [""]

        # Add existing options (in the order they appear)
        for opt in existing:
            if opt and opt not in new_list:
                new_list.append(opt)

        # Add required options if missing
        for opt in required_options:
            if opt not in new_list:
                new_list.append(opt)

        final_value = "\n".join(new_list)

        frappe.db.set_value("Property Setter", ps.name, "value", final_value)
        frappe.db.commit()

    else:
        # No Property Setter exists yet → create new one
        new_list = [""] + required_options

        frappe.get_doc({
            "doctype": "Property Setter",
            "doctype_or_field": "DocField",
            "doc_type": doctype,
            "field_name": fieldname,
            "property": "options",
            "property_type": "Text",
            "value": "\n".join(new_list)
        }).insert(ignore_permissions=True)

    frappe.clear_cache(doctype=doctype)

import frappe

def execute():
	for dt in ('BOM', 'Work Order', 'Stock Entry'):
		frappe.reload_doctype(dt)

	frappe.db.sql("""
	UPDATE
		`tabBOM`
	SET
		manufacturing_type = "Discrete"
	WHERE
		manufacturing_type IS NULL
""")

	frappe.db.sql("""
	UPDATE
		`tabWork Order`
	SET
		manufacturing_type = "Discrete"
	WHERE
		manufacturing_type IS NULL
""")

	frappe.db.sql("""
	UPDATE
		`tabStock Entry`
	SET
		manufacturing_type = "Discrete"
	WHERE
		manufacturing_type IS NULL
""")
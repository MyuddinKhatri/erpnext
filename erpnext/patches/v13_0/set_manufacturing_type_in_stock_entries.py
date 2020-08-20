import frappe

def execute():
	frappe.db.sql("""
	UPDATE
		`tabStock Entry`
	SET
		manufacturing_type = "Discrete"
	WHERE
		manufacturing_type IS NULL
""")
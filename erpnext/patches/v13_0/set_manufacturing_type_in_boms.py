import frappe

def execute():
	frappe.db.sql("""
	UPDATE
		`tabBOM`
	SET
		manufacturing_type = "Discrete"
	WHERE
		manufacturing_type IS NULL
""")
import frappe

def execute():
	frappe.db.sql("""
	UPDATE
		`tabWork Order`
	SET
		manufacturing_type = "Discrete"
	WHERE
		manufacturing_type IS NULL
""")
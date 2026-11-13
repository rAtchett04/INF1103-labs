class Supplier:
    # Represents a supplier for products
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        # Displays supplier details
        print(f"Supplier ID: {self.supplier_id} | Name: {self.name} | Email: {self.contact_email}")

    def to_dict(self) -> dict:
        # Converts Supplier instance to dictionary for JSON persistence.
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> "Supplier":
        # Creates a Supplier instance from a dictionary
        if not data:
            return cls("SUP000", "Main Supplier", "mainsupplier@example.com")
        return cls(
            supplier_id=data.get("supplier_id", "SUP000"),
            name=data.get("name", "Main Supplier"),
            contact_email=data.get("contact_email", "N/A")
        )
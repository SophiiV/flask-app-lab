from flask import Blueprint, render_template, abort

products_bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
)

# Простий in-memory "каталог"
PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 29.9},
    {"id": 2, "name": "Mouse", "price": 19.5},
    {"id": 3, "name": "Monitor", "price": 199.0},
]

@products_bp.route("/")
def list_products():
    return render_template(
        "products/list.html",
        page_title="Products",
        content_title="Products List",
        products=PRODUCTS,
    )

@products_bp.route("/<int:pid>")
def product_detail(pid):
    item = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not item:
        abort(404)
    return render_template(
        "products/detail.html",
        page_title=f"Product #{pid}",
        content_title=f"Product #{pid}",
        product=item,
    )

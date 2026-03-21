# Global Components

Edit these files to change UI elements across the site. All pages that use these components will update automatically.

| Component | File | Where used |
|-----------|------|------------|
| **Header** | `header.html` | All pages (via base.html) |
| **Footer** | `footer.html` | All pages (via base.html) |
| **Car Card** | `car_card.html` | Home (featured, recent), Car list, Wishlist |
| **CTA Section** | `cta.html` | Home page (Sell Your Car banner) |

## Car Card variants

- **Carousel** (default): Home page carousels, AJAX responses
- **Grid**: Car list page — use `{% include 'partials/car_card.html' with car=car wishlisted_ids=wishlisted_ids variant="grid" %}`

## CTA Section

Include anywhere: `{% include 'partials/cta.html' %}`

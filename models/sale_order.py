from odoo import models, fields
from odoo.exceptions import UserError
import requests
import json
import urllib.parse

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # =========================
    # FIELDS
    # =========================
    razorpay_payment_link_id = fields.Char("Razorpay Payment Link ID")
    payment_link = fields.Char("Payment Link", readonly=True)

    payment_status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ], string="Payment Status", default='draft', tracking=True)

    # =========================
    # GENERATE PAYMENT LINK
    # =========================
    def action_generate_payment(self):
        self.ensure_one()

        # ✅ 1. Validate state
        if self.state != 'sale':
            raise UserError("Confirm the Sales Order first.")

        # ✅ 2. Prevent duplicate link
        if self.payment_link:
            return {
                'type': 'ir.actions.act_url',
                'url': self.payment_link,
                'target': 'new',
            }

        # ✅ 3. Get Razorpay keys
        key_id = self.env['ir.config_parameter'].sudo().get_param('razorpay.key_id')
        key_secret = self.env['ir.config_parameter'].sudo().get_param('razorpay.key_secret')

        if not key_id or not key_secret:
            raise UserError("Razorpay keys not configured.")

        # =========================
        # 4. BUILD CUSTOMER DATA (NO PHONE REQUIRED)
        # =========================
        customer_data = {
            "name": self.partner_id.name or "Customer"
        }

        # add email only if available
        if self.partner_id.email:
            customer_data["email"] = self.partner_id.email

        # =========================
        # 5. CREATE PAYMENT LINK
        # =========================
        url = "https://api.razorpay.com/v1/payment_links"

        payload = {
            "amount": int(self.amount_total * 100),
            "currency": "INR",
            "description": f"Payment for {self.name}",
            "customer": customer_data,
            "notify": {
                "sms": False,   # ✅ disable SMS (no phone)
                "email": True
            },
            "reminder_enable": True
        }

        try:
            response = requests.post(
                url,
                auth=(key_id, key_secret),
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code not in [200, 201]:
                raise UserError(f"Razorpay Error:\n{response.text}")

            data = response.json()

        except requests.exceptions.RequestException as e:
            raise UserError(f"Connection Error: {str(e)}")

        # =========================
        # 6. SAVE DATA
        # =========================
        self.payment_link = data.get('short_url')   # 🔥 real Razorpay link
        self.razorpay_payment_link_id = data.get('id')
        self.payment_status = 'pending'

        # =========================
        # 7. OPEN PAYMENT PAGE
        # =========================
        return {
            'type': 'ir.actions.act_url',
            'url': self.payment_link,
            'target': 'new',
        }

    import urllib.parse

    def action_send_whatsapp(self):
        self.ensure_one()

        if not self.payment_link:
            raise UserError("Generate payment link first.")

        # ✅ Safe phone fetch (no mobile dependency)
        phone = self.partner_id.phone

        if not phone:
            raise UserError("Customer phone number not found.")

        # clean number
        phone = phone.replace(" ", "").replace("+", "")

        # message
        message = f"""
        Hello {self.partner_id.name},

        🧾 Order: {self.name}
        💰 Amount: ₹{self.amount_total}

        📦 Items:
        {', '.join(self.order_line.mapped('product_id.name'))}

        🔗 Payment Link:
        {self.payment_link}

        Kindly complete the payment at your earliest convenience.

        Thank you!
        """

        encoded_message = urllib.parse.quote(message)

        whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"

        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }
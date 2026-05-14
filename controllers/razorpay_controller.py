from odoo import http
from odoo.http import request


class RazorpayController(http.Controller):

    @http.route('/razorpay/pay/<int:order_id>', type='http', auth='user', website=True)
    def razorpay_payment(self, order_id, **kwargs):

        order = request.env['sale.order'].sudo().browse(order_id)

        return request.render('weather.payment_page_template', {
            'order': order,
            'key_id': 'rzp_test_SdetdnQlFGFLIw',
        })


    @http.route('/razorpay/success', type='http', auth='user', website=True)
    def razorpay_success(self, **kwargs):

        order_id = kwargs.get('order_id')

        order = request.env['sale.order'].sudo().search([
            ('razorpay_order_id', '=', order_id)
        ])

        if order:
            order.payment_status = 'paid'

        return request.redirect('/web')
odoo.define('mobile_device_reception.key_events', function (require) {
    "use strict";

    var Widget = require('web.AbstractField');

    var AbstractField = Widget.include({
        _onNavigationMove: function (ev) {
            ev.data.target = this;
            $(this.$el[0]).blur();
            $(this.$el[0]).focus();
        },
    });
});
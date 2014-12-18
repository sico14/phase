var Phase = Phase || {};

(function(exports, Phase, Backbone, _) {
    "use strict";

    var dispatcher = Phase.Events.dispatcher;

    Phase.Views = Phase.Views || {};

    Phase.Views.NotificationsModalView = Backbone.View.extend({
        el: '#notifications-modal',
        events: {
            'show.bs.modal': 'loadNotifications',
            'click button.more': 'loadNotifications'
        },
        initialize: function() {
            this.body = this.$el.find('.notifications');
            this.moreBtn = this.$el.find('button.more');

            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'add', this.addNotification);
            this.listenTo(this.collection, 'updateNextUrl', this.updateNextUrl);
        },
        loadNotifications: function(events) {
            this.collection.fetch();
        },
        render: function() {
            this.collection.each(this.addNotification);
            return true;
        },
        addNotification: function(notification) {
            var view = new Phase.Views.NotificationItemView({ model: notification });
            this.body.append(view.render().el);
        },
        updateNextUrl: function(url) {
            if (url === null) {
                this.moreBtn.hide();
            }
        }
    });

    Phase.Views.NotificationItemView = Backbone.View.extend({
        tagName: 'div',
        className: 'notification',
        template: _.template($('#tpl-notification').html()),
        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        }
    });

})(this, Phase, Backbone, _);

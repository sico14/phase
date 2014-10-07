var Phase = Phase || {};

(function(exports, Phase, Backbone, _) {
    "use strict";

    Phase.Models = {};

    Phase.Models.Document = Backbone.Model.extend({
        idAttribute: 'pk'
    });

    Phase.Models.Favorite = Backbone.Model.extend({});

    /**
     * Represents a single search query set of parameters
     */
    Phase.Models.Search = Backbone.Model.extend({
        defaults: {
            search_terms: '',
            sort_by: 'document_key',
            start: 0,
            size: Phase.Config.paginateBy
        },
        fromForm: function(form) {
            var data = form.serializeArray();
            self = this;
            _.each(data, function(field) {
                self.set(field.name, field.value);
            });
        },
        nextPage: function() {
            var start = this.get('start');
            var size = this.get('size');
            this.set('start', start + size);
        },
        reset: function() {
            this.set('start', this.defaults.start);
            this.set('size',  this.defaults.size);
        }
    });

})(this, Phase, Backbone, _);
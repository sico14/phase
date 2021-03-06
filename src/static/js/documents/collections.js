var Phase = Phase || {};

(function(exports, Phase, Backbone, _) {
    "use strict";

    Phase.Collections = Phase.Collections || {};

    Phase.Collections.DocumentCollection = Backbone.Collection.extend({
        model: Phase.Models.Document,
        url: Phase.Config.searchUrl,
        parse: function(response) {
            this.total = response.total;
            this.aggregations = response.aggregations;
            return response.data;
        }
    });

})(this, Phase, Backbone, _);

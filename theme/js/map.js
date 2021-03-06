// Generated by CoffeeScript 1.10.0
(function() {
  var SpotMap, ce, d, getQueryString;

  d = React.DOM;

  ce = React.createElement;

  getQueryString = function() {
    var hash, hashes, i, key, len, qs, qsi, sep, sri, val, vars;
    vars = [];
    qsi = window.location.href.indexOf("?");
    if (qsi === -1) {
      return vars;
    }
    qs = window.location.href.slice(qsi + 1);
    sri = qs.indexOf("#");
    if (sri >= 0) {
      qs = qs.slice(0, sri);
    }
    hashes = qs.split("&");
    for (i = 0, len = hashes.length; i < len; i++) {
      hash = hashes[i];
      sep = hash.indexOf("=");
      if (sep <= 0) {
        continue;
      }
      key = decodeURIComponent(hash.slice(0, sep));
      val = decodeURIComponent(hash.slice(sep + 1));
      vars[key] = val;
    }
    return vars;
  };

  SpotMap = React.createFactory(React.createClass({
    displayName: "SpotMap",
    defaultPublicToken: "pk.eyJ1IjoicmphbWVzODYiLCJhIjoiY2ltam53d2F5MDBzZnY4a2cyaWR4Y3pnMyJ9.SM84_1rqm7WiwAl4uO7RIw",
    propTypes: {
      activity: React.PropTypes.object
    },
    getInitialState: function() {
      return {
        feed_id: this.getFeedId(),
        coords: [],
        photos: []
      };
    },
    componentDidMount: function() {
      var myMapObj;
      myMapObj = {
        center: [46.8787176, -113.996586],
        zoom: 5.83
      };
      window.mymap = L.map('map', myMapObj);
      this.generateMapTile();
      if (this.state.feed_id != null) {
        $.getJSON("https://dl.dropboxusercontent.com/s/0u9acsrnxqv1w9g/tracking_info.json", (function(_this) {
          return function(res) {
            var coords;
            coords = _.where(res, {
              feed_id: _this.state.feed_id
            });
            return _this.setState({
              coords: coords
            }, _this.addPolyline);
          };
        })(this));
        return $.getJSON("https://dl.dropboxusercontent.com/s/aekt6faujrfewhm/photo_info.json", (function(_this) {
          return function(res) {
            return _this.setState({
              photos: res
            }, _this.addPhotos);
          };
        })(this));
      }
    },
    getFeedId: function() {
      var queryString;
      queryString = getQueryString();
      return queryString.feed_id;
    },
    createPopUps: function() {
      var i, item, len, marker, markers, ref;
      markers = L.markerClusterGroup();
      ref = this.state.coords;
      for (i = 0, len = ref.length; i < len; i++) {
        item = ref[i];
        marker = new L.marker([item.latitude, item.longitude]).bindPopup("" + item.datetime, {
          minWith: 100
        });
        markers.addLayer(marker);
      }
      window.mymap.addLayer(markers);
      return this.setMapView();
    },
    setMapView: function() {
      var first, last, ref;
      if (this.state.coords.length) {
        ref = this.state.coords, first = ref[0], last = ref[ref.length - 1];
        return window.mymap.setView(new L.LatLng(last.latitude, last.longitude), 15);
      }
    },
    createIcon: function(url) {
      return L.icon({
        iconUrl: url,
        iconSize: [32, 32]
      });
    },
    addPhotos: function() {
      var i, item, len, marker, markers, ref, results;
      markers = L.markerClusterGroup();
      ref = this.state.photos;
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        item = ref[i];
        if ((item.latitude == null) || (item.image_url == null)) {
          continue;
        }
        marker = new L.marker([item.latitude, item.longitude], {
          icon: this.createIcon(item.thumbnail)
        }).bindPopup("<img src='" + item.image_url + "'><p>Taken " + item.time_taken + " Pacific</p>", {
          minWidth: 640
        });
        markers.addLayer(marker);
        results.push(window.mymap.addLayer(markers));
      }
      return results;
    },
    addPolyline: function() {
      var item, latLngs;
      latLngs = (function() {
        var i, len, ref, results;
        ref = this.state.coords;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          item = ref[i];
          results.push([item.latitude, item.longitude]);
        }
        return results;
      }).call(this);
      this.polyline = L.polyline(latLngs, {
        color: "red"
      }).addTo(window.mymap);
      return this.createPopUps();
    },
    generateMapTile: function() {
      return L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=" + this.defaultPublicToken, {
        maxZoom: 18,
        accessToken: this.defaultPublicToken
      }).addTo(window.mymap);
    },
    render: function() {
      return d.div({
        className: "map-container",
        style: {
          "height": window.innerHeight + "px"
        }
      }, d.div({
        id: "map"
      }));
    }
  }));

  $(function() {
    var react_content;
    react_content = document.getElementById('widget');
    return ReactDOM.render(ce(SpotMap, null, null), react_content);
  });

}).call(this);

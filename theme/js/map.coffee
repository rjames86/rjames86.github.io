d = React.DOM
ce = React.createElement

getQueryString = ->
  vars = []

  # Get the start index of the query string
  qsi = window.location.href.indexOf("?")
  return vars if qsi is -1

  # Get the query string
  qs = window.location.href.slice(qsi + 1)

  # Check if there is a subsection reference
  sri = qs.indexOf("#")
  qs = qs.slice(0, sri) if sri >= 0

  # Build the associative array
  hashes = qs.split("&")
  for hash in hashes
    sep = hash.indexOf("=")
    continue if sep <= 0
    key = decodeURIComponent(hash.slice(0, sep))
    val = decodeURIComponent(hash.slice(sep + 1))
    vars[key] = val

  vars


SpotMap = React.createFactory React.createClass
  displayName: "SpotMap"
  defaultPublicToken: "pk.eyJ1IjoicmphbWVzODYiLCJhIjoiY2ltam53d2F5MDBzZnY4a2cyaWR4Y3pnMyJ9.SM84_1rqm7WiwAl4uO7RIw"
  propTypes:
    activity: React.PropTypes.object

  getInitialState: ->
    feed_id: @getFeedId()
    coords: []
    photos: []

  componentDidMount: ->
    myMapObj =
      center: [46.8787176, -113.996586] # Missoula, MT
      zoom: 5.83
    window.mymap = L.map('map', myMapObj)
    @generateMapTile()

    if @state.feed_id?
      $.getJSON "https://dl.dropboxusercontent.com/s/0u9acsrnxqv1w9g/tracking_info.json", (res) =>
        coords = _.where res, feed_id: @state.feed_id
        @setState coords: coords, @addPolyline

      $.getJSON "https://dl.dropboxusercontent.com/s/aekt6faujrfewhm/photo_info.json", (res) =>
        @setState photos: res, @addPhotos

  getFeedId: ->
    queryString = getQueryString()
    queryString.feed_id

  createPopUps: ->
    markers = L.markerClusterGroup()

    for item in @state.coords
      marker = new L.marker [item.latitude, item.longitude]
        .bindPopup("#{item.datetime}", {minWith: 100})
      markers.addLayer marker
    window.mymap.addLayer markers
    @setMapView()

  setMapView: ->
    if @state.coords.length
      [first, ..., last] = @state.coords
      window.mymap.setView new L.LatLng(last.latitude, last.longitude), 15

  createIcon: (url) ->
    L.icon
      iconUrl: url,
      iconSize: [32, 32],

  addPhotos: ->
    for item in @state.photos
      if not item.latitude? or not item.image_url?
        continue
      marker = new L.marker [item.latitude, item.longitude], {icon: @createIcon(item.thumbnail)}
        .bindPopup("<img src='#{item.image_url}'><p>Taken #{item.time_taken} Pacific</p>", {minWidth: 320})
        .addTo(window.mymap)

  addPolyline: ->
    latLngs = ([item.latitude, item.longitude] for item in @state.coords)
    @polyline = L.polyline(latLngs, {color: "red"}).addTo(window.mymap)
    @createPopUps()

  generateMapTile: ->
    L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=#{@defaultPublicToken}", {
      maxZoom: 18,
      accessToken: @defaultPublicToken
    }).addTo(window.mymap)

  render: ->
    d.div
      className: "map-container",
      style: {"height": "#{window.innerHeight}px"}
    ,
      d.div id: "map"


$ ->
  react_content = document.getElementById('widget')
  ReactDOM.render(ce(SpotMap, null, null), react_content)

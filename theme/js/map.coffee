d = React.DOM
ce = React.createElement

SpotMap = React.createFactory React.createClass
  displayName: "SpotMap"
  defaultPublicToken: "pk.eyJ1IjoicmphbWVzODYiLCJhIjoiY2ltam53d2F5MDBzZnY4a2cyaWR4Y3pnMyJ9.SM84_1rqm7WiwAl4uO7RIw"
  propTypes:
    activity: React.PropTypes.object

  getInitialState: ->
    coords: []
    photos: []

  componentDidMount: ->
    myMapObj =
      center: [46.8787176, -113.996586] # Missoula, MT
      zoom: 5.83
    window.mymap = L.map('map', myMapObj)

    $.getJSON "https://dl.dropboxusercontent.com/s/0u9acsrnxqv1w9g/tracking_info.json", (res) =>
      @setState coords: res, =>
        @generateMapTile()
        @addPolyline()

    $.getJSON "https://dl.dropboxusercontent.com/s/aekt6faujrfewhm/photo_info.json", (res) =>
      @setState photos: res, @addPhotos

  createPopUps: ->
    for item in @state.coords
      marker = new L.marker [item.latitude, item.longitude]
        .bindPopup("#{item.datetime}", {minWith: 100})
        .addTo(window.mymap)

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
    if @state.coords.length
      [first, ..., last] = @state.coords
      window.mymap.setView new L.LatLng(last.latitude, last.longitude), 15

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

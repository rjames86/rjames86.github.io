d = React.DOM
ce = React.createElement

SpotMap = React.createFactory React.createClass
  displayName: "SpotMap"
  defaultPublicToken: "pk.eyJ1IjoicmphbWVzODYiLCJhIjoiY2ltam53d2F5MDBzZnY4a2cyaWR4Y3pnMyJ9.SM84_1rqm7WiwAl4uO7RIw"
  propTypes:
    activity: React.PropTypes.object

  coords: null
  photos: null
  mymap: null

  parseCoords: ->
    ret = []
    for item in @coords
      ret.push [item.latitude, item.longitude]
    ret

  createPopUps: ->
    for item in @coords
      marker = new L.marker [item.latitude, item.longitude]
        .bindPopup("#{item.datetime}", {minWith: 100})
        .addTo(window.mymap)

  createIcon: (url) ->
    L.icon
      iconUrl: url,
      iconSize: [32, 32],

  addPhotos: ->
    for item in @photos
      if not item.latitude?
        continue
      marker = new L.marker [item.latitude, item.longitude], {icon: @createIcon(item.thumbnail)}
        .bindPopup("<img src='#{item.image_url}'>", {minWidth: 320})
        .addTo(window.mymap)

  addLayer: ->
    @polyline = L.polyline(@parseCoords(), {color: "red"}).addTo(window.mymap)
    # mymap.fitBounds(@polyline.getBounds())
    @createPopUps()

  componentDidMount: ->
    myMapObj =
      center: [46.8787176, -113.996586] # Missoula, MT
      zoom: 5.83
    window.mymap = L.map('map', myMapObj)

    $.ajax
      url: "https://dl.dropboxusercontent.com/s/0u9acsrnxqv1w9g/tracking_info.json",
      success: (res) =>
        @coords = JSON.parse res
        if @coords.length
          [first, ..., last] = @coords
          console.log last.latitude, last.longitude
          window.mymap.setView new L.LatLng(last.latitude, last.longitude), 15

        L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=#{@defaultPublicToken}", {
          maxZoom: 18,
          accessToken: @defaultPublicToken
        }).addTo(window.mymap)
        console.log "mymap", window.mymap
        @addLayer()

    $.ajax
      url: "https://dl.dropboxusercontent.com/s/aekt6faujrfewhm/photo_info.json",
      success: (res) =>
        @photos = JSON.parse res
        @addPhotos()

  render: ->
    d.div
      className: "map-container",
      style: {"height": "#{window.innerHeight}px"}
    ,
      d.div id: "map"


$ ->
  react_content = document.getElementById('widget')
  ReactDOM.render(ce(SpotMap, null, null), react_content)

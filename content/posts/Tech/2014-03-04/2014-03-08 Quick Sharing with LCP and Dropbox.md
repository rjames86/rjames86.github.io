Title: Quick Sharing with Launch Center Pro and Dropbox
Date: 2014-03-04
Category: Tech
Tags: ios, automation, Dropbox, launchcenterpro, photos
Author: Ryan M

I've been finding more and more reasons to use Launch Center Pro recently. With the fairly recent addition of Dropbox actions, I've been finding new ways to share links quickly. 
<!-- PELICAN_END_SUMMARY -->  

![Launch Center Pro and Dropbox]({attach}lcp_dropbox.png)

I take a lot of quick photos that I never plan to keep around. In most cases, it's just to send to someone quickly. iMessage is easy, but the images aren't compressed nearly enough and can take a while to upload. I've now started uploading the images to Dropbox and sharing the link. The upload speed is reduced since Launch Center Pro will take care of reducing the quality before uploading. The message sends almost instantly because there isn't an attachment. Here are a few of workflows I use with Dropbox:

### Upload last photo taken and get the link
*This is if I simply need a quick link to share anywhere. The image uploads at 50% quality. I have a folder called Temp/_Destrctable Folder where I keep all my throwaway images. I'm using the TextExpander snippet ..ttimestamp to name the files like 14-03-08-19.42.45.jpg*

	launchpro-dropbox://addlastphoto?path=/Temp/_Destructable Folder&name=<..ttimestamp>.jpg&quality=50&getlink=1

### Upload last photo and put the link in an in-app message body
*Quick sharing with iMessage. Settings are the same as above.* 

	launch://x-callback-url/dropbox/addphoto?attach=photo&path=/Temp/_Destructable Folder&name=<..ttimestamp>.jpg&quality=50&getlink=1&x-success=launch%3A//messaging%3Fbody%3D%5Bclipboard%5D

###  Upload from any source to Dropbox
*Nice if you haven't taken the photo yet*

	launch://dropbox/addphoto?attach=photo&path=&name=&quality=&getlink=1

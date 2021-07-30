Title: Using Dropbox to Host Images on your Website
Date: 2013-11-03
Category: Tech
Tags: dropbox, scripting
Slug: dropboxsharedlinks
Author: Ryan M

I notice a lot of people asking about why they can't get images to display on their website when using [Dropbox shared links][sharedlinks]. Dropbox is a great way to post an image quickly on a forum or as free hosting for your low traffic website, but there are a few things to know.
<!-- PELICAN_END_SUMMARY -->  

[sharedlinks]: https://www.dropbox.com/help/167

In the early days, Dropbox offered a Public folder where you could easily serve webpages, images or anything else you want to share to the world. The risk there is that the links to the files were formulaic and anyone could crawl your Public folder looking for things they maybe shouldn't have. This formula looked like this:

www.dropbox.com/u/<number\>/<name of file\>

To add a level of security to the shared links, Dropbox now has a hashed value so that someone would then need to know the unique hash as well as the file name. The chances that someone is able to guess both of these within the next 10,000 years is pretty low. The second thing that was added was a preview to your shared links. If you have images, you see a nice gallery in your links and Office documents now have a preview. The downside here is that simple file hosting doesn't work by pasting in the link.

To solve this, you just need to change the actual shared link with the link to the file itself. To do this, you just need to replace `www.dropbox.com` with `dl.dropboxusercontent.com`. This will serve the true file instead of the file wrapped in a preview. For those of you using snippet software like TextExpander, you can make this a lot faster by making a shell script snippet with the following:

{! dbl.sh !}
    
Now an image like

https://www.dropbox.com/s/kyjm1pr79g2irfj/Guinness%20Storehouse%20top.jpg

turns into this:

![https://dl.dropboxusercontent.com/s/kyjm1pr79g2irfj/Guinness%20Storehouse%20top.jpg](https://dl.dropboxusercontent.com/s/kyjm1pr79g2irfj/Guinness%20Storehouse%20top.jpg)

[sampleimage]: https://www.dropbox.com/s/jq8xvuvikx90o9y/Guinness%20Storehouse%20top.jpg

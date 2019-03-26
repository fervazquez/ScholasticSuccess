let PDF2Pic=require('pdf2pic').default
let converter= PDF2Pic({
    density:100,
    savename:"hold",
    savedir:"./images",
    format:"jpg",
    size:600
})

converter.convertBulk("02172019.pdf",-1)
    .then(resolve=>{
        console.log("image held in images")
    })
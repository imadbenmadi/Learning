const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.static("public")); // Serve static files from public directory

app.get("/video", (req, res) => {
    const videoPath = path.join(__dirname, "public", "videos", "sample.mp4"); // Path to the video file
    const videoStat = fs.statSync(videoPath);
    const fileSize = videoStat.size;
    const range = req.headers.range;

    if (range) {
        const parts = range.replace(/bytes=/, "").split("-");
        const start = parseInt(parts[0], 10);
        const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
        const chunkSize = end - start + 1;
        const file = fs.createReadStream(videoPath, { start, end });
        const head = {
            "Content-Range": `bytes ${start}-${end}/${fileSize}`,
            "Accept-Ranges": "bytes",
            "Content-Length": chunkSize,
            "Content-Type": "video/mp4",
        };
        res.writeHead(206, head);
        file.pipe(res);
    } else {
        const head = {
            "Content-Length": fileSize,
            "Content-Type": "video/mp4",
        };
        res.writeHead(200, head);
        fs.createReadStream(videoPath).pipe(res);
    }
    // Cashing the video
    res.set({
        "Cache-Control": "public, max-age=31536000", // Cache for 1 year
    });
});
// Optimized video streaming with headers
app.get("/Courses_Videos/:videoName", (req, res) => {
    const videoName = req.params.videoName;
    const videoPath = path.join(
        __dirname,
        "public",
        "Courses_Videos",
        videoName
    );

    fs.stat(videoPath, (err, stat) => {
        if (err) {
            console.error("File not found:", err);
            return res.status(404).send("Video not found");
        }

        const fileSize = stat.size;
        const range = req.headers.range;

        // Set caching headers
        res.setHeader("Cache-Control", "public, max-age=31536000");
        res.setHeader("Accept-Ranges", "bytes");

        if (range) {
            const parts = range.replace(/bytes=/, "").split("-");
            const start = parseInt(parts[0], 10);
            const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
            const chunkSize = end - start + 1;
            const file = fs.createReadStream(videoPath, { start, end });

            res.writeHead(206, {
                "Content-Range": `bytes ${start}-${end}/${fileSize}`,
                "Content-Length": chunkSize,
                "Content-Type": "video/mp4",
            });
            file.pipe(res);
        } else {
            res.writeHead(200, {
                "Content-Length": fileSize,
                "Content-Type": "video/mp4",
            });
            fs.createReadStream(videoPath).pipe(res);
        }
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

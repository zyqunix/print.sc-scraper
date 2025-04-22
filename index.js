const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');
const os = require('os');

const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
const screenshotsDir = path.join(__dirname, 'screenshots');
if (!fs.existsSync(screenshotsDir)) fs.mkdirSync(screenshotsDir);

function* generateIds() {
    for (let a of chars)
    for (let b of chars)
    for (let c of chars)
    for (let d of chars)
    for (let e of chars) {
        yield `${a}${b}${c}${d}${e}`;
    }
}

async function fetchAndSave(idCode) {
    const url = `https://prnt.sc/${idCode}`;
    const headers = { 'User-Agent': 'Mozilla/5.0' };

    try {
        const res = await axios.get(url, { headers, timeout: 10000 });
        const $ = cheerio.load(res.data);
        const img = $('img.no-click.screenshot-image');
        const imgUrl = img.attr('src');

        if (!imgUrl || !imgUrl.startsWith('http')) {
            console.log(`[${idCode}] No valid image found.`);
            return;
        }

        const imgRes = await axios.get(imgUrl, { headers, responseType: 'arraybuffer' });
        if (imgRes.status === 200) {
            const ext = path.extname(imgUrl).split('?')[0].replace('.', '') || 'jpg';
            const filePath = path.join(screenshotsDir, `${idCode}.${ext}`);
            fs.writeFileSync(filePath, imgRes.data);
            console.log(`[${idCode}] Saved.`);
        } else {
            console.log(`[${idCode}] Image URL returned ${imgRes.status}.`);
        }
    } catch (e) {
        console.log(`[${idCode}] Error: ${e.message}`);
    }
}

async function main() {
    const concurrency = 50;
    const queue = [];
    for (const id of generateIds()) {
        queue.push(fetchAndSave(id));
        if (queue.length >= concurrency) {
            await Promise.all(queue.splice(0, concurrency));
        }
    }
    await Promise.all(queue);
}

main();

const express = require('express');
const app = express();
const path = require('path');
const port = 5400;
const http = require('http');
const $ = require('jquery');
const querystring = require('querystring');

app.use

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static('../Web/views'));
app.use(express.static('../Web/css'));
app.use(express.static('../Web/image'));

app.get('/', (req, res) => {
    res.render('index.ejs'); // 렌더링할 EJS 템플릿 파일의 이름 (index.ejs)
});

app.get('/index2', (req, res) => {
    res.render('index2.ejs');
});


app.get('/showtexts', (req, res) => {
    const predClass = req.query.pred_class;
    console.log("인공지능 결과 : " + predClass);

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/getnoun/?class=' + querystring.escape(predClass),
        method: 'GET'
    };

    const clientReq = http.request(options, (response) => {
        let nouns = '';

        response.on('data', (chunk) => {
            nouns += chunk;
        });

        response.on('end', () => {
            console.log('다른 서버로부터의 응답: ' + nouns);
            nouns = nouns.replace(/"/g, '').replace("[", '').replace("]", '');
            nouns = nouns.split(', ');
            res.render('show_texts.ejs', {"nouns": nouns});
        });
    });

    clientReq.end();
});

app.get('/input_send', (req, res) => {
    const inputText = req.query.text;

    console.log('입력 텍스트: ', inputText);

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/predtext/?text=' + querystring.escape(inputText),
        method: 'GET'
    };

    const clientReq = http.request(options, (response) => {
        let responseData = '';

        response.on('data', (chunk) => {
            responseData += chunk;
        });

        response.on('end', () => {
            console.log('다른 서버로부터의 응답: ' + responseData);
            res.send(responseData);
        });
    });

    clientReq.end();
});

app.listen(port, '0.0.0.0', () => {
    console.log("server is open");
});

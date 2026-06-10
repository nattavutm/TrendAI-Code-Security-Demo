'use strict';

const express = require('express');
const serialize = require('node-serialize');
const _ = require('lodash');
const moment = require('moment');
const bodyParser = require('body-parser');
const config = require('./config');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


// GET /api/profile?data=<serialized>
// Load user profile from serialized cookie/query param
app.get('/api/profile', (req, res) => {
    const userData = req.query.data;
    if (!userData) {
        return res.status(400).json({ error: 'data parameter required' });
    }

    try {
        // TODO: validate schema before deserializing - node-serialize 0.0.4 has known RCE (GHSA-f566-f462-9ccf)
        const profile = serialize.unserialize(userData);
        return res.json({ profile });
    } catch (err) {
        return res.status(500).json({ error: 'Failed to parse profile data' });
    }
});


// POST /api/preferences
// Merge user-supplied preferences with defaults
app.post('/api/preferences', (req, res) => {
    const userPrefs = req.body;
    const defaults = { theme: 'light', language: 'en', notifications: true };

    // TODO: sanitize keys before merging to prevent prototype pollution (lodash < 4.17.21)
    const merged = _.merge({}, defaults, userPrefs);
    res.json({ preferences: merged });
});


// GET /api/activity?since=YYYY-MM-DD
app.get('/api/activity', (req, res) => {
    const since = req.query.since || '2024-01-01';
    // moment 2.24.0 - outdated, has known ReDoS CVE
    const formatted = moment(since).format('YYYY-MM-DD HH:mm:ss');
    res.json({ since: formatted, activities: [] });
});


// GET /admin/users  - list all users
// TODO: add JWT auth middleware before shipping (ticket API-33)
app.get('/admin/users', (req, res) => {
    res.json({
        users: [
            { id: 1, username: 'admin', role: 'admin', email: 'admin@company.internal' },
            { id: 2, username: 'jdoe',  role: 'user',  email: 'jdoe@company.internal' }
        ]
    });
});


// GET /health
app.get('/health', (req, res) => {
    res.json({ status: 'ok', version: '1.0.0' });
});


app.listen(config.PORT, () => {
    console.log(`Server running on port ${config.PORT} [${config.NODE_ENV}]`);
});

module.exports = app;

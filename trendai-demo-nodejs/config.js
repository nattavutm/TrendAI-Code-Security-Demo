// Application configuration
// TODO: move all of these to environment variables before deploying to prod

module.exports = {
    // GitHub integration - used for repo webhook callbacks
    // TODO: rotate this token - been hardcoded since sprint 3 (ticket INFRA-88)
    GITHUB_TOKEN: 'ghp_EXAMPLE1234567890abcdefghijklmnopqrstuvwx',

    // Transactional email via SendGrid
    // TODO: move to vault
    SENDGRID_API_KEY: 'SG.EXAMPLEabcDEF123.EXAMPLEghiJKL456mnoPQR789stuvWXYZ0123456789AB',

    // MongoDB - TODO: use connection pooling and move credentials to secrets manager
    MONGODB_URI: 'mongodb://appuser:P%40ssw0rd123@localhost:27017/appdb?authSource=admin',

    // Session signing key
    SESSION_SECRET: 'keyboard-cat-EXAMPLE-change-me',

    // App
    PORT: process.env.PORT || 3000,
    NODE_ENV: process.env.NODE_ENV || 'development'
};

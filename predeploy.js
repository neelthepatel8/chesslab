const { exec } = require("child_process");

const commands = ["docker compose down"];

commands.forEach((cmd) => {
    exec(cmd, (error, stdout, stderr) => {
        if (stdout) console.log(`stdout: ${stdout}`);
        if (stderr) console.log(`stderr: ${stderr}`);
    });
});


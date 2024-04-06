const log = (...messages) => {
  if (process.env.NODE_ENV !== "production") {
    console.log(...messages);
  }
};

export default log;

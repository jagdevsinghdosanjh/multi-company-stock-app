const { restClient } = require("@polygon.io/client-js");

const rest = restClient(process.env.POLYGON_API_KEY);

module.exports = async (req, res) => {
  const { ticker } = req.query;

  if (!ticker) {
    return res.status(400).json({ error: "Ticker is required" });
  }

  try {
    const data = await rest.stocks.aggregates(
      ticker.toUpperCase(),
      1,
      "day",
      "2025-01-01",
      "2025-05-11"
    );
    res.status(200).json(data);
  } catch (e) {
    res.status(500).json({ error: "An error occurred: " + e.message });
  }
};

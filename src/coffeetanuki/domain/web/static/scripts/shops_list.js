// Fetch data from the API and populate the shop list
fetch("/api/shops")
  .then((response) => response.json())
  .then((data) => {
    const shopList = document.getElementById("shops-list");

    data.forEach((shop) => {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = "/shops/" + shop.id; // Assuming you have a separate HTML page for each shop, passing the shop ID as a query parameter
      link.textContent = shop.name;

      // Add Tailwind CSS classes
      li.className = "list-disc ml-4";
      link.className = "text-blue-500 font-bold hover:text-blue-700";

      li.appendChild(link);
      shopList.appendChild(li);
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });

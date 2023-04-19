import React, { useState, useEffect } from "react";

function Obituaries({ obituaries }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const options = { month: "long", day: "numeric", year: "numeric" };
    return date.toLocaleDateString("en-US", options);
  };

  const [activeObituaryIndices, setActiveObituaryIndices] = useState([]);

  useEffect(() => {
    // Set the most recent obituary as active by default
    const mostRecentObituary = obituaries.length > 0 ? obituaries[0] : null;
    if (mostRecentObituary) {
      setActiveObituaryIndices([obituaries.indexOf(mostRecentObituary)]);
    }
  }, [obituaries]);

  const handleObituaryClick = (index) => {
    if (activeObituaryIndices.includes(index)) {
      // If the clicked obituary is active, remove it from the active obituaries
      setActiveObituaryIndices(activeObituaryIndices.filter((i) => i !== index));
    } else {
      // If the clicked obituary is not active, set it as active
      setActiveObituaryIndices([...activeObituaryIndices, index]);
    }
  };

  return (
    <div className="obituariesContainer">
      {obituaries.map((obituary, index) => (
        <div
          className="obituaryBox"
          key={index}
          onClick={() => handleObituaryClick(index)}
          style={{
            height: activeObituaryIndices.includes(index) ? "auto" : "250px",
            marginTop: !activeObituaryIndices.includes(index) ? "0px" : "0", //can be adjusted later
          }}
        >
          <img className="deceasedImage" src={obituary.file} alt="Obituary Image" />
          <p className="deceasedName">{obituary.name}</p>
          <p className="lifeLength">
            {formatDate(obituary.birth)} - {formatDate(obituary.death)}
          </p>
          {activeObituaryIndices.includes(index) && (
            <p className="description">{obituary.description}</p>
          )}
        </div>
      ))}
    </div>
  );
}

export default Obituaries;

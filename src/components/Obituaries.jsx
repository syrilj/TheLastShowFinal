import React, {useState} from "react";
import Obituary from "./Obituary";

function Obituaries({ obituaries }) {
  

  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 items-start">
      {obituaries.map((obituary, index) => (
        <Obituary
          key={index}
          id={index}
          name={obituary.name}
          birth={obituary.birth}
          cloudinary_url={obituary.cloudinary_url}
          death={obituary.death}
          description={obituary.description}
          polly_url={obituary.polly_url}

        />
      ))}
    </div>
  );
}

export default Obituaries;


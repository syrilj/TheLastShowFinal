import React, { useState, useEffect } from "react";
import { FaPlay, FaPause } from "react-icons/fa";


function Obituary({ name, birth, cloudinary_url, death, description, polly_url, id }) {
  const formatDate = (Userdate) => {
    const date = new Date(Userdate);
    const monthNames = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    const month = monthNames[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month} ${day}, ${year}`;
  };

  const [showDescription, setShowDescription] = useState(false);
  const [descriptionHeight, setDescriptionHeight] = useState("0px");

  const handleToggleDescription = () => {
    setShowDescription(!showDescription);
  };

  useEffect(() => {
    if (showDescription) {
      setDescriptionHeight(`${document.getElementById(`description-inner-${id}`).scrollHeight}px`);
    } else {
      setDescriptionHeight("0px");
    }
  }, [showDescription, description, id]);

  const [isPlaying, setIsPlaying] = useState(false);
  const [audioElement, setAudioElement] = useState(null);

  const createAudioElement = () => {
    const audio = new Audio(polly_url);
    audio.onended = () => setIsPlaying(false);
    setAudioElement(audio);
    return audio;
  };

  const handlePlayPauseClick = () => {
    if (!audioElement) {
      createAudioElement().play();
      setIsPlaying(true);
    } else if (isPlaying) {
      audioElement.pause();
      setIsPlaying(false);
    } else {
      audioElement.play();
      setIsPlaying(true);
    }
  };

  return (
    <div className="max-w-sm rounded overflow-hidden shadow-lg inline-block">
      <img className="w-full hover:opacity-95" src={cloudinary_url} alt="obituary"  onClick={handleToggleDescription}/>
      <div className="px-6 py-2 flex flex-col justify-center items-center">
        <h2 className="font-bold text-xl mb-2">{name}</h2>
        <p className="text-gray-700 text-base mb-2">
          {formatDate(birth)} - {formatDate(death)}
        </p>
        <div
          className="overflow-hidden transition-all duration-500 ease-in-out"
          style={{ height: descriptionHeight}}
        >
          <div id={`description-inner-${id}`}>
            <p className="text-gray-700 text-lg mb-2" style={{ fontFamily: "Satisfy" }}>{description}</p>
            <div className="mt-2 flex justify-center ">
              <button
                className="bg-black text-white font-bold py-4 px-4 rounded-full hover:bg-gray-700"
                onClick={handlePlayPauseClick}
              >
                {isPlaying ? <FaPause /> : <FaPlay />}
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Obituary;



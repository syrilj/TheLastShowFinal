import { useState } from "react";
import { Link } from "react-router-dom";
import WriteNew from "./WriteNew";

const Header = ({obituaries, setObituaries, uuid}) => {
  const [showModal, setShowModal] = useState(false);

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <header className="flex justify-center items-center border-b-2 px-6 py-4 mb-2">
      <div className="text-center flex-1">
        <Link to="/">
          <h1 className="text-2xl font-bold">The Last Show</h1>
        </Link>
      </div>
      <div
        className="hover:bg-gray-600 hover:text-white flex items-center border-2 border-gray-600 rounded-md p-2 cursor-pointer"
        onClick={handleOpenModal}
      >
        <h2 className="text-sm">+ New Obituary</h2>
      </div>
      {showModal && (
        <div className="fixed top-0 left-0 w-full h-full opacity-95 ">
          <div className="absolute w-full h-full  p-6 bg-white rounded-md shadow-lg">
            <div className="flex justify-end">
              <button
                className="p-2 hover:bg-gray-200 rounded-full"
                onClick={handleCloseModal}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            <WriteNew handleCloseModal={handleCloseModal} obituaries={obituaries} uuid={uuid} setObituaries={setObituaries}></WriteNew>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;


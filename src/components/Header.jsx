import { Link } from "react-router-dom"

const Header = () => {
  return (
    <header className="flex justify-center items-center border-b-2 px-6 py-4 mb-2">
      <div className="text-center flex-1">
        <Link to="/">
          <h1 className="text-2xl font-bold">The Last Show</h1>
        </Link>
      </div>
      <div className="hover:bg-gray-600 hover:text-white flex items-center border-2 border-gray-600 rounded-md p-2">
        <Link to="/newObituary">
          <h2 className="text-sm ">+ New Obituary</h2>
        </Link>
      </div>
    </header>


  )
}

export default Header
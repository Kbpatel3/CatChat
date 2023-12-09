/**
 * Search bar component for searching for users
 * @param onChange - function to call when the search query changes
 * @returns {JSX.Element} - Search bar component
 */
function SearchBar({ onChange }) {
    /**
     * Handles the search query changing when the user types in the search bar
     * @param e - event object for the search bar which contains the search query
     */
  const handleSearchChange = (e) => {
    console.log('Search query:', e.target.value)
    // TODO: Send the search query to the server via the socket connection
  }

  return (
    <div className="w-full h-full flex items-center justify-center">
      <input
        type="text"
        placeholder="Search for User"
        onChange={handleSearchChange}
        className="p-2 border border-gray-300 rounded w-full"
      />
    </div>
  );
}

export default SearchBar;

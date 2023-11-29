function SearchBar({ onChange }) {
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

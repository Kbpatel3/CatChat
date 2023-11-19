const chatList = () => {
    const chatButtons = [
        {id: 1, label: 'Chat 1'},
        {id: 2, label: 'Chat 2'},
        {id: 3, label: 'Chat 3'},
        {id: 4, label: 'Chat 4'},
        {id: 5, label: 'Chat 5'},
    ]

    const handleClick = (id) => {
        // Handle click here
    }

    return (
        <>
            <div>   {/* Most likely needs to be fleshed out more */}
                {chatButtons.map((button) => (
                    <button onClick={() => handleClick(button.id)}>{button.label}</button>
                ))}
            </div>
        </>
    )
}
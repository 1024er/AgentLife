

const SelectAvatarButton = ({
  characters,
  selectedAvatar,
  setSelectedAvatar
}) => {
  return (
    <div className="flex space-x-4">
      {characters.map((character, index) => (
        <button
          key={index}
          className={`p-4 py-2 rounded-full text-white drop-shadow-md cursor-pointer transition-colors text-sm ${
            selectedAvatar === character.id ? "bg-slate-800" : "bg-slate-500 hover:bg-slate-800"
          }`}
          onClick={() => {
            setSelectedAvatar(character.id);
          }}
        >
          {character.gender == "male" ? "♂" : "♀"} {character.name} （id: {character.id}）
        </button>
      ))}
    </div>
  )
};

export default SelectAvatarButton;
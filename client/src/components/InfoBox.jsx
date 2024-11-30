import React from 'react'

const InfoBox = ({
    characters,
    selectedAvatar
}) => {
  return (
    <div className="fixed right-5 top-5 w-80 h-2/5 flex flex-col items-start space-y-2 p-0 bg-opacity-30 shadow-lg rounded-lg text-xs overflow-y-auto backdrop-blur-sm duration-500" style={{ userSelect: 'none' }}>
    {characters?.find(character => character.id === selectedAvatar) ? (
        <table className="table-auto">
        <tbody>
        {Object.entries(characters.find(character => character.id === selectedAvatar))
            .filter(([key]) => !['id', 'session', 'avatarName', 'path', 'event', 'max_energe', 'current_energe', 'max_hunger', 'current_hunger', 'energe_change', 'hunger_change', 'gender', 'position', 'look_at', 'max_memory'].includes(key))
            .map(([key, value], index) => (
            <tr key={key} className={index % 2 === 0 ? 'bg-gray-600 bg-opacity-30' : 'bg-gray-0 bg-opacity-50'}>
                <td className="px-4 py-2 text-sky-100">{key}</td>
                <td className="px-4 py-2 text-sky-100">
                {JSON.stringify(value)}
                </td>
            </tr>
        ))}
        </tbody>
        </table>
    ) : (
        <div className="p-2 text-red-400">角色信息不可用</div>
    )}
    </div>
  )
}

export default InfoBox
        cur.execute("SELECT id, name, address FROM users")
        users = cur.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(users), 200

# Update User Address
@app.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json(silent=True)
    if not data or 'address' not in data:
        return jsonify({'error': 'Invalid or missing JSON: address required'}), 400

    address = data['address']

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET address = %s WHERE id = %s",
            (address, user_id)
        )
        if cur.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'User address updated successfully'}), 200

# Delete User
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        if cur.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    # Use PORT env var if set, otherwise default to 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

